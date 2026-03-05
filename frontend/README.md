# Frontend (Next.js)

PhishGuard frontend — URL тексеру интерфейсі, нәтиже визуализациясы, auth және history беттері.

## Орнату

```bash
cd frontend
npm install
```

## Іске қосу

```bash
npm run dev
```

App: `http://localhost:3000`

## Build

```bash
npm run lint
npm run build
npm run start
```

## API байланысы

`src/lib/api.ts` ішінде API base қазір hardcoded:

```ts
const API_BASE = "http://localhost:8000/api/v1";
```

Егер backend басқа host/port-та тұрса, осы мәнді өзгертіңіз.

## Негізгі беттер

- `/` — сканерлеу беті
- `/login` — кіру
- `/register` — тіркелу
- `/history` — сканерлеу тарихы

## UI стиль бағыты

- Ақ-сұр-қара минималистік дизайн
- Жеңіл шекаралар, жұмсақ көлеңке, таза типографика
- Mobile + desktop responsive

