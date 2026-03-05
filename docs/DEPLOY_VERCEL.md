# Deploy Frontend to Vercel (Backend on Railway)

Бұл сценарий:

- Backend: Railway (`https://phishing.up.railway.app`)
- Frontend: Vercel

## 1) Backend тексеру (Railway)

Backend health тексеріңіз:

- `https://phishing.up.railway.app/`
- `https://phishing.up.railway.app/docs`

## 2) Vercel-ге frontend импорт

1. Vercel -> `Add New...` -> `Project`
2. GitHub репо таңдаңыз: `Azamaperdeev05/phishing`
3. `Root Directory` ретінде `frontend` таңдаңыз

## 3) Vercel Environment Variable

Project Settings -> Environment Variables:

- `NEXT_PUBLIC_API_BASE_URL = https://phishing.up.railway.app/api/v1`

Сосын redeploy жасаңыз.

## 4) Railway CORS жаңарту

Backend service (`phishing`) Variables ішінде:

- `PHISHGUARD_CORS_ORIGINS=https://<your-vercel-domain>,http://localhost:3000`

Мысалы:

`PHISHGUARD_CORS_ORIGINS=https://phishguard.vercel.app,http://localhost:3000`

## 5) Тексеру

1. Vercel URL ашыңыз
2. URL scan жасап көріңіз
3. Browser console-да CORS қатесі жоқ екеніне көз жеткізіңіз

