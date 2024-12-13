import sounddevice as sd
import numpy as np
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

# إعدادات الصوت
sample_rate = 44100  # معدل العينة
duration = 10  # مدة التسجيل (بالثواني)
pitch_factor = 1.0  # عامل تغيير النبرة (1.0 = بدون تغيير)
volume_factor = 1.0  # عامل تضخيم الصوت (1.0 = بدون تغيير، >1.0 = تضخيم)
distortion_factor = 0.0  # عامل التشويش (0.0 = بدون تأثير، >0.0 = إضافة تشويش)
compression_factor = 0.5  # عامل الضغط الديناميكي

stream = None  # المتغير الذي سيحمل تدفق الصوت


def pitch_shift(data, factor):
    """تغيير النبرة عبر تغيير معدل العينة"""
    indices = np.round(np.arange(0, len(data), factor))
    indices = indices[indices < len(data)].astype(int)
    return data[indices]


def add_distortion(data, factor):
    """إضافة تشويش للصوت"""
    noise = np.random.normal(0, factor, data.shape)
    distorted_data = data + noise
    return np.clip(distorted_data, -1.0, 1.0)


def apply_compression(data, factor):
    """تطبيق التضخيم الديناميكي"""
    # حساب مستوى الصوت الأقصى (الحد الأقصى للبيانات)
    peak = np.max(np.abs(data))
    if peak > 0:
        # تطبيق الضغط لتقليل الفرق بين أعلى وأدنى مستويات الصوت
        data = np.clip(data, -peak * factor, peak * factor)
    return data


def callback(indata, outdata, frames, time, status):
    """معالجة الصوت في الوقت الفعلي"""
    if status:
        print(status)
    # تغيير النبرة
    processed = pitch_shift(indata[:, 0], pitch_factor)
    # تضخيم الصوت
    amplified = processed * volume_factor
    # إضافة تأثير التشويش
    distorted = add_distortion(amplified, distortion_factor)
    # تطبيق الضغط الديناميكي
    compressed = apply_compression(distorted, compression_factor)
    # التأكد من أن الإشارة لا تتجاوز الحدود المقبولة
    compressed = np.clip(compressed, -1.0, 1.0)
    # إخراج الصوت
    outdata[: len(compressed), 0] = compressed
    outdata[len(compressed) :, 0] = 0


class VoiceChangerApp(App):
    def build(self):
        global pitch_factor, volume_factor, distortion_factor, compression_factor, stream

        # واجهة المستخدم باستخدام Kivy
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # إضافة شريط تمرير لتغيير النبرة
        pitch_label = Label(text="Pitch Factor")
        self.pitch_slider = Slider(min=1.0, max=2.0, value=1.0)
        self.pitch_slider.bind(value=self.update_pitch_factor)

        # إضافة شريط تمرير لتغيير حجم الصوت
        volume_label = Label(text="Volume Factor")
        self.volume_slider = Slider(min=0.5, max=100.0, value=1.0)
        self.volume_slider.bind(value=self.update_volume_factor)

        # إضافة شريط تمرير لتغيير التشويش
        distortion_label = Label(text="Distortion Factor")
        self.distortion_slider = Slider(min=0.0, max=1.0, value=0.0)
        self.distortion_slider.bind(value=self.update_distortion_factor)

        # إضافة شريط تمرير لتغيير التضخيم الديناميكي
        compression_label = Label(text="Compression Factor")
        self.compression_slider = Slider(min=0.0, max=1.0, value=0.5)
        self.compression_slider.bind(value=self.update_compression_factor)

        # إضافة زر لبدء المعالجة
        start_button = Button(text="Start Voice Processing")
        start_button.bind(on_press=self.start_processing)

        # إضافة زر لإيقاف المعالجة
        stop_button = Button(text="Stop Voice Processing")
        stop_button.bind(on_press=self.stop_processing)

        # إضافة كل العناصر إلى الواجهة
        layout.add_widget(pitch_label)
        layout.add_widget(self.pitch_slider)
        layout.add_widget(volume_label)
        layout.add_widget(self.volume_slider)
        layout.add_widget(distortion_label)
        layout.add_widget(self.distortion_slider)
        layout.add_widget(compression_label)
        layout.add_widget(self.compression_slider)
        layout.add_widget(start_button)
        layout.add_widget(stop_button)

        # إضافة حقوق المستخدم
        rights_label = Label(text="Rights Reserved by Asgard (Telegram: @asgard_0)")
        layout.add_widget(rights_label)

        return layout

    def update_pitch_factor(self, instance, value):
        global pitch_factor
        pitch_factor = value

    def update_volume_factor(self, instance, value):
        global volume_factor
        volume_factor = value

    def update_distortion_factor(self, instance, value):
        global distortion_factor
        distortion_factor = value

    def update_compression_factor(self, instance, value):
        global compression_factor
        compression_factor = value

    def start_processing(self, instance):
        global stream
        if stream is None or not stream.active:
            # تشغيل التسجيل والمعالجة في الوقت الفعلي
            stream = sd.Stream(channels=1, samplerate=sample_rate, callback=callback)
            stream.start()
            print("Recording and processing... Speak now!")

    def stop_processing(self, instance):
        global stream
        if stream is not None and stream.active:
            # إيقاف تدفق الصوت
            stream.stop()
            print("Processing stopped.")


if __name__ == "__main__":
    VoiceChangerApp().run()
