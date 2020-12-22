import contextlib
import os
import tempfile

ui = R'''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Dialog</class>
 <widget class="QDialog" name="Dialog">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>569</width>
    <height>368</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Dialog</string>
  </property>
  <widget class="QLabel" name="label">
   <property name="geometry">
    <rect>
     <x>110</x>
     <y>20</y>
     <width>81</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Account</string>
   </property>
  </widget>
  <widget class="QLabel" name="label_2">
   <property name="geometry">
    <rect>
     <x>110</x>
     <y>50</y>
     <width>81</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Password</string>
   </property>
  </widget>
  <widget class="QPushButton" name="testLoginBtn">
   <property name="geometry">
    <rect>
     <x>350</x>
     <y>30</y>
     <width>113</width>
     <height>32</height>
    </rect>
   </property>
   <property name="text">
    <string>test login</string>
   </property>
  </widget>
  <widget class="QPushButton" name="showEnrolledBtn">
   <property name="geometry">
    <rect>
     <x>100</x>
     <y>320</y>
     <width>113</width>
     <height>32</height>
    </rect>
   </property>
   <property name="text">
    <string>show enrolled</string>
   </property>
  </widget>
  <widget class="QPushButton" name="downloadBtn">
   <property name="geometry">
    <rect>
     <x>310</x>
     <y>320</y>
     <width>151</width>
     <height>32</height>
    </rect>
   </property>
   <property name="text">
    <string>download enrolled</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="account">
   <property name="geometry">
    <rect>
     <x>210</x>
     <y>20</y>
     <width>113</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QLineEdit" name="password">
   <property name="geometry">
    <rect>
     <x>210</x>
     <y>50</y>
     <width>113</width>
     <height>21</height>
    </rect>
   </property>
   <property name="echoMode">
    <enum>QLineEdit::Password</enum>
   </property>
  </widget>
  <widget class="QTextBrowser" name="log">
   <property name="geometry">
    <rect>
     <x>80</x>
     <y>90</y>
     <width>411</width>
     <height>211</height>
    </rect>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>'''


@contextlib.contextmanager
def get_ui_filename():
    with tempfile.TemporaryDirectory() as d:
        filename = os.path.join(d, 'ilmsdump.ui')
        with open(filename, 'w') as file:
            file.write(ui)
        yield filename
