import { useState, useRef, useEffect } from 'react';
import type { BankService } from '../data/mockServices';
import { cosineSimilarity } from '../modules/math';

export interface IProcessedBankService extends BankService {
    score: number;
    isVisible: boolean;
    embedding?: number[];
}

export const useBankServiceSearch = (initialItems: BankService[]) => {
    const [items, setItems] = useState<IProcessedBankService[]>(
        initialItems.map(item => ({ ...item, score: 0, isVisible: true, embedding: undefined }))
    );
    const [imageEmbedding, setImageEmbedding] = useState<number[] | null>(null);
    const [ready, setReady] = useState(false);
    const [progress, setProgress] = useState(0);
    const workerRef = useRef<Worker | null>(null);

    // Синхронизация при изменении initialItems
    useEffect(() => {
        setItems(initialItems.map(item => ({ ...item, score: 0, isVisible: true, embedding: undefined })));
    }, [initialItems]);

    // Инициализация воркера и вычисление текстовых эмбеддингов
    useEffect(() => {
        if (initialItems.length === 0) return;

        const hasDescriptions = initialItems.every(item => item.english_description);
        if (!hasDescriptions) {
            console.warn('Некоторые услуги не имеют english_description, поиск может работать некорректно');
        }

        workerRef.current = new Worker(new URL('../workers/search.worker.ts', import.meta.url), { type: 'module' });
        workerRef.current.onmessage = (e) => {
            const { type, data } = e.data;
            switch (type) {
                case 'progress':
                    if (data.status === 'progress') setProgress(data.progress);
                    else if (data.status === 'ready') setReady(true);
                    break;
                case 'text_embeddings_ready':
                    setItems(prev => prev.map(item => ({
                        ...item,
                        embedding: data[item.id]
                    })));
                    setReady(true);
                    break;
                case 'image_embedding_ready':
                    setImageEmbedding(data);
                    break;
                case 'error':
                    console.error('Worker error:', data);
                    setReady(false);
                    break;
            }
        };

        const workerData = initialItems.map(item => ({
            id: item.id,
            english_description: item.english_description ?? ''
        }));
        workerRef.current.postMessage({ type: 'init', data: workerData });

        return () => workerRef.current?.terminate();
    }, [initialItems]);

    const searchByImage = (file: File) => {
        workerRef.current?.postMessage({ type: 'image', data: file });
    };

    const resetSearch = () => {
        setImageEmbedding(null);
        setItems(prev => {
            const sortedById = [...prev].sort((a, b) => a.id - b.id);
            return sortedById.map(item => ({ ...item, score: 0, isVisible: true }));
        });
    };

    useEffect(() => {
        if (!imageEmbedding) return;
        setItems(prevItems => {
            if (!prevItems[0]?.embedding) return prevItems;
            const threshold = 0.005;
            const processed = prevItems.map(item => {
                if (!item.embedding) return { ...item, score: 0, isVisible: false };
                const similarity = cosineSimilarity(imageEmbedding, item.embedding);
                return { ...item, score: similarity, isVisible: similarity > threshold };
            });

            processed.sort((a, b) => b.score - a.score);
            const TOP_K = 4;   // максимальное количество результатов
            return processed.slice(0, TOP_K);
        });
    }, [imageEmbedding]);

    return {
        items,
        ready,
        progress,
        imageEmbedding,
        searchByImage,
        resetSearch,
    };
};