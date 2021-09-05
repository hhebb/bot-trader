from PyQt5.QtWidgets import *

'''
    [GUI 분류 체계]
    > 범위별 분류, 기능별 분류 2 가지 방법.
    1. 단일 widget 은 기본 widget 으로 사용한다.
        * 스타일, 서식 등은 QWidget 단에서 모두 지원 가능하기 때문.
    2. 2 개 이상 widget 이 조합되면 새로운 class 를 만든다.
        * 웬만하면 frame 단위로 만들어서 frame 꾸미기 쉽도록 만들 수 있음.
        * 대부분 기본 widget 이 frame 직계자손.
        * 새로 정의되는 기능(메서드)과 새로 추가된 데이터 입출력(signal, slot) 을 커스텀하기 쉽도록 만듬.
        * 각 내부 아이템(widget, frame) 들은 layout 혹은 splitter 에 의해 배치 조정 되도록 함.
    3. [2] 에서 이미 정의한 클래스 안에 widget 을 더 추가하고 싶을 땐 상속을 한다.
        * base class 를 만들어서 상속을 한다.
    4. [2] 에서 이미 정의한 클래스와 비슷한데 기능의 차이가 있다면 한 단계 추상화 한다.
        * base class 를 만들어서 각각 상속을 한다.
        * 웬만하면 base class 는 인스턴스를 만들지 않고 abc 를 사용.
    5. 하나의 아이템으로 독립성을 띌 수 있으면 이름에 container 를 붙인다.
        * 여러 아이템들을 감싸고 기능들을 포함하는 하나의 모듈로서 인식.
        * panel 이나 도구모음 등에 사용하기에 적합하다.
        * 어디까지 widget 이고 어디까지 container 라고 할 지 모호함이 있다.
        * 기능은 제외하고 배치에 관한 영역이라고만 생각하면 될 듯.
    
    
    [설계]
    * 시각적으로 bottom-up 설계.
    * 작은 아이템부터 쌓아 올리는 방법.
    * 먼저 가장 작은 item 을 정의하고 점점 살을 붙여가며 정의함.
    * GUI 도 변동성이 적은 core widget, 변동성이 빈번한 배치(container)나 상속받은 widget 계층이 있음.
    * 크게 3 종류의 클래스
        1. base
        2. base 들의 조합, 그 조합들의 조합. 일반 widget
        3. container
        
'''


class BaseTable(QFrame):
    def __init__(self, parent):
        super().__init__(parent)


class BaseTableItem(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

