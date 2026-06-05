export const mockServices: BankService[] = [
  {
    id: 1,
    name: "Кредит для бизнеса",
    balance_account: "40701",
    description: "Кредит на покупку оборудования, пополнение оборотных средств",
    image: "SoftPOS-01.jpg",   // проверьте, что этот файл есть в папке img
    video: "credit.mp4",       // исправлено
    price: 1500,
    created_at: "2024-10-01T10:30:00Z",
  },
  {
    id: 2,
    name: "Расчетный счет для бизнеса",
    balance_account: "40702",
    description: "Открытие онлайн, бесплатные переводы",
    image: "rko_2_mor.webp",
    video: "RKO.mp4",          // исправлено (обратите внимание на регистр!)
    price: 0,
    created_at: "2024-09-15T09:00:00Z",
  },
  {
    id: 3,
    name: "Кредитная карта",
    balance_account: "40801",
    description: "Кэшбэк до 5%, льготный период до 100 дней",
    image: "logo-cent.JPG",
    video: "credit_card.mp4",   // исправлено
    price: 0,
    created_at: "2024-10-10T14:15:00Z",
  },
  {
    id: 4,
    name: "Депозит",
    balance_account: "40703",
    description: "Вклад с ежемесячной капитализацией, ставка до 12%",
    image: "null",
    video: "deposit.mp4",       // исправлено
    price: 0,
    created_at: "2024-11-01T11:00:00Z",
  },
  {
    id: 5,
    name: "Эквайринг",
    balance_account: "40704",
    description: "Приём платежей по картам и СБП",
    image: "logo-burger.JPG",
    video: "acquiring.mp4",     // исправлено
    price: 0,
    created_at: "2024-11-05T10:00:00Z",
  },
  {
    id: 6,
    name: "Тест_бизнес_ипотека",
    balance_account: "40800",
    description: "Ипотека для юридических лиц",
    image: "home2.jpg",
    video: "ipoteka.mp4",       // исправлено
    price: 0,
    created_at: "2024-11-10T12:00:00Z",
  },
];