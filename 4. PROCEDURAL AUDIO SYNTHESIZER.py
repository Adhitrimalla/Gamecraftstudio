4. PROCEDURAL AUDIO SYNTHESIZER
# =============================================================================
class SoundManager:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.sounds = {}
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self._generate_sounds()
        except Exception:
            pass

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled

    def _generate_sine_wav(self, tones, duration=0.2, volume=0.3):
        sample_rate = 22050
        num_samples = int(sample_rate * duration)
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            frames = bytearray()
            for i in range(num_samples):
                t = i / sample_rate
                val = 0.0
                for freq, amp in tones:
                    val += math.sin(2 * math.pi * freq * t) * amp
                fade = max(0.0, 1.0 - (i / num_samples))
                sample = int(max(-32767, min(32767, val * 32767 * volume * fade)))
                frames.extend(struct.pack('<h', sample))
            wav.writeframes(frames)
        buf.seek(0)
        return pygame.mixer.Sound(buf)

    def _generate_noise_wav(self, duration=0.3, volume=0.35):
        sample_rate = 22050
        num_samples = int(sample_rate * duration)
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            frames = bytearray()
            for i in range(num_samples):
                fade = max(0.0, 1.0 - (i / num_samples))
                val = random.uniform(-1.0, 1.0) * fade * volume
                sample = int(max(-32767, min(32767, val * 32767)))
                frames.extend(struct.pack('<h', sample))
            wav.writeframes(frames)
        buf.seek(0)
        return pygame.mixer.Sound(buf)

    def _generate_sounds(self):
        try:
            self.sounds["coin"] = self._generate_sine_wav([(987, 0.5), (1318, 0.5)], duration=0.18, volume=0.35)
            self.sounds["super_coin"] = self._generate_sine_wav([(659, 0.4), (880, 0.4), (1318, 0.5)], duration=0.30, volume=0.45)
            self.sounds["magnet"] = self._generate_sine_wav([(523, 0.4), (784, 0.4), (1046, 0.5)], duration=0.28, volume=0.4)
            self.sounds["booster"] = self._generate_sine_wav([(523, 0.5), (659, 0.5), (1046, 0.4)], duration=0.25, volume=0.4)
            self.sounds["star"] = self._generate_sine_wav([(1046, 0.5), (1318, 0.5)], duration=0.25, volume=0.45)
            self.sounds["victory"] = self._generate_sine_wav([(523, 0.3), (659, 0.3), (784, 0.3), (1046, 0.5)], duration=0.65, volume=0.55)
            self.sounds["fail"] = self._generate_sine_wav([(392, 0.4), (329, 0.4), (261, 0.5)], duration=0.5, volume=0.45)
            self.sounds["crash"] = self._generate_noise_wav(duration=0.42, volume=0.55)
            self.sounds["nitro"] = self._generate_noise_wav(duration=0.25, volume=0.3)
            self.sounds["click"] = self._generate_sine_wav([(880, 0.3)], duration=0.08, volume=0.25)
        except Exception:
            pass

    def play(self, name):
        if not self.enabled:
            return
        if name in self.sounds:
            try:
                self.sounds[name].play()
            except Exception:
                pass
