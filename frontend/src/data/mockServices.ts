// src/data/mockServices.ts

export interface BankService {
  id: number;
  name: string;
  balance_account: string;
  description: string;
  image: string | null;
  video: string | null;
  price: number;
  created_at: string;
  english_description: string;   // для CLIP
}

export const mockServices: BankService[] = [
  {
    id: 1,
    name: "Кредит для бизнеса",
    balance_account: "40701",
    description: "Кредит на покупку оборудования, пополнение оборотных средств",
    image: "SoftPOS-01.jpg",
    video: "credit.mp4",
    price: 1500,
    created_at: "2024-10-01T10:30:00Z",
    english_description: "Business loan for equipment purchase and working capital"
  },
  {
    id: 2,
    name: "Расчетный счет для бизнеса",
    balance_account: "40702",
    description: "Открытие онлайн, бесплатные переводы",
    image: "rko_2_mor.webp",
    video: "RKO.mp4",
    price: 0,
    created_at: "2024-09-15T09:00:00Z",
    english_description: "Online business account opening with free transfers"
  },
  {
    id: 3,
    name: "Кредитная карта",
    balance_account: "40801",
    description: "Кэшбэк до 5%, льготный период до 100 дней",
    image: "logo-cent.JPG",
    video: "credit_card.mp4",
    price: 0,
    created_at: "2024-10-10T14:15:00Z",
    english_description: "Credit card with 5% cashback and 100-day interest-free period"
  },
  {
    id: 4,
    name: "Депозит",
    balance_account: "40703",
    description: "Вклад с ежемесячной капитализацией, ставка до 12%",
    image: "null",
    video: "deposit.mp4",
    price: 0,
    created_at: "2024-11-01T11:00:00Z",
    english_description: "Deposit with monthly interest capitalization, up to 12% rate"
  },
  {
    id: 5,
    name: "Эквайринг",
    balance_account: "40704",
    description: "Приём платежей по картам и СБП",
    image: "logo-burger.JPG",
    video: "acquiring.mp4",
    price: 0,
    created_at: "2024-11-05T10:00:00Z",
    english_description: "Card and SBP payment acquiring for businesses"
  },
  {
    id: 6,
    name: "Тест_бизнес_ипотека",
    balance_account: "40800",
    description: "Ипотека для юридических лиц",
    image: "home2.jpg",
    video: "ipoteka.mp4",
    price: 0,
    created_at: "2024-11-10T12:00:00Z",
    english_description: "Commercial mortgage for legal entities"
  }
];