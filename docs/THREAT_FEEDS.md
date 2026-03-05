# Threat Feeds

## Мақсаты

Фишинг анықтауды үнемі өзекті ету үшін сыртқы threat-intel фидтерден домендер жүктеледі.

## Қолданылатын көздер

- URLhaus recent text feed  
  `https://urlhaus.abuse.ch/downloads/text_recent/`
- OpenPhish community feed  
  `https://openphish.com/feed.txt`

## Жаңарту

```bash
cd backend
python scripts/update_threat_feeds.py
```

Нәтиже файлы:

- `backend/data/threat_feed_domains.json`

JSON ішінде:

- `generated_at_utc`
- `source_stats`
- `domain_count`
- `domains`

## Ұсынылатын жиілік

- Production: әр 6 сағат сайын
- Development: күніне 1 рет

## Ескерту

Feed-based blacklist match қазір нақты hostname негізінде жасалады.  
Бұл shared-hosting платформаларда жаппай false-positive болдырмау үшін.

