import pygame

class CustomSound:
    all_sounds = []
    vol_sound = 1

    def __init__(self, filename: str, volume: int = 1) -> None:
        """
        Класс для звуков для более удобной настройки громкости
        :param filename: Путь к файлу
        :type filename: str
        :param volume: Стандартная громкость звука
        :type volume: int
        """
        self.all_sounds.append(self)
        self.sound = pygame.mixer.Sound(filename)
        self.volume = volume
        # выставляем громкости
        self.sound.set_volume(volume)
        self.set_default_volume(self.vol_sound)

    def set_volume(self, volume: int) -> None:
        """
        Установка громкости
        :param volume: Громкость
        :type volume: int
        """
        self.volume = volume
        self.sound.set_volume(volume)

    def set_default_volume(self, new_volume: int) -> None:
        """
        Поставить громкость, выбранную пользователем
        :param new_volume: Громкость из настроек
        :type new_volume: int
        """
        self.sound.set_volume(self.volume * new_volume)

    def play(self, *args, **kwargs) -> None:
        """
        Проигрывание звука
        """
        self.sound.play(*args, **kwargs)

    def stop(self) -> None:
        """
        Остановить проигрывание звука
        """
        self.sound.stop()

    def fadeout(self, *args, **kwargs) -> None:
        """
        Плавная остановка проигрывания звука
        """
        self.sound.fadeout(*args, **kwargs)