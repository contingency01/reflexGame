# Refleks Oyunu

Bu proje, tepki sürenizi ölçen basit bir Pygame uygulamasıdır.

## Çalıştırma

1. Bağımlılıkları yükleyin:

```bash
pip install -r requirements.txt
```

2. Oyunu başlatın:

```bash
python main.py
```

## Oynanış

- Ana menüde oyunu başlatabilir veya uygulamayı kapatabilirsiniz. Fareyle üzerlerine gelindiğinde düğmeler vurgulanır.
- **Başla** seçeneğine tıkladıktan sonra turun ne kadar süreceğini seçebilirsiniz.
- Oyun sırasında ekranın ortasındaki daire her 4 saniyede bir renk değiştirir. Daire yeşile döndüğünde mümkün olduğunca hızlı bir şekilde **Space** tuşuna basın, ardından daire anında başka bir renge geçer.
- Sağ üst köşedeki **Kapat** düğmesi oyundan erken çıkmanızı sağlar.
- Oyun sonrasında sonuçlar otomatik olarak kaydedilir ve ana menüdeki **Leaderboard** bölümünden önceki oturumların ortalamalarını ve tüm tepki sürelerini görebilirsiniz.
