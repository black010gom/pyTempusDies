from datetime import datetime, timedelta
from kivy.app import App
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior

# NanumGothic 폰트 등록 (현재 경로에 NanumGothic.ttf 파일이 있어야 함)
LabelBase.register(name="NanumGothic", fn_regular="NanumGothic.ttf")

DATE_FMT = "%Y-%m-%d"

def parse_date(s: str):
    try:
        return datetime.strptime(s.strip(), DATE_FMT)
    except Exception:
        return None

# Hover 기능 구현
class HoverLabel(ButtonBehavior, Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_enter=self._on_enter, on_leave=self._on_leave)

    def _on_enter(self, *args):
        # 마우스가 올라왔을 때 힌트 표시
        print(f"Hint: {self.text}")

    def _on_leave(self, *args):
        # 마우스가 벗어났을 때 힌트 숨김
        print("Hint 숨김")

# Long press 버튼 구현
class LongPressButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._event = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # 2.5초 이상 누르면 long press 이벤트 발생
            self._event = Clock.schedule_once(self._long_press, 2.5)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self._event:
            self._event.cancel()
        return super().on_touch_up(touch)

    def _long_press(self, dt):
        print(f"Long press Hint: {self.text}")

class TestApp(App):
    title = "날짜 계산기"

    def build(self):
        # 창 크기 설정
        Window.size = (480, 600)
        return Builder.load_file("tempusdies.kv")

    def switch_screen(self, name: str):
        sm = self.root
        sm.current = name

    def _set_result(self, screen_name: str, label_id: str, text: str):
        screen = self.root.get_screen(screen_name)
        screen.ids[label_id].text = text

    # 특정 날짜부터 특정 날짜까지의 일수 계산
    def calc_days_between(self, start_text: str, end_text: str):
        d1 = parse_date(start_text)
        d2 = parse_date(end_text)
        if not d1 or not d2:
            self._set_result("days_between", "result_between", "입력 오류: YYYY-MM-DD 형식으로 입력하세요.")
            return
        delta = (d2 - d1).days
        self._set_result("days_between", "result_between", f"총 {delta}일")

    # 특정 날짜와 일수로부터 며칠 후 날짜 계산
    def calc_days_after(self, base_text: str, days_text: str):
        d = parse_date(base_text)
        try:
            days = int(days_text.strip())
        except Exception:
            days = None
        if not d or days is None:
            self._set_result("days_after", "result_after", "입력 오류: 날짜는 YYYY-MM-DD, 일수는 정수로 입력하세요.")
            return
        result = d + timedelta(days=days)
        self._set_result("days_after", "result_after", f"결과 날짜: {result.strftime(DATE_FMT)}")

    # 특정 날짜와 일수로부터 며칠 전 날짜 계산
    def calc_days_before(self, base_text: str, days_text: str):
        d = parse_date(base_text)
        try:
            days = int(days_text.strip())
        except Exception:
            days = None
        if not d or days is None:
            self._set_result("days_before", "result_before", "입력 오류: 날짜는 YYYY-MM-DD, 일수는 정수로 입력하세요.")
            return
        result = d - timedelta(days=days)
        self._set_result("days_before", "result_before", f"결과 날짜: {result.strftime(DATE_FMT)}")

if __name__ == "__main__":
    TestApp().run()
