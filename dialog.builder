<?xml version="1.0"?>
<interface>
  <requires lib="gtk+" version="2.16"/>
  <!-- interface-naming-policy project-wide -->
  <object class="GtkDialog" id="Dialog">
    <property name="border_width">5</property>
    <property name="title" translatable="yes">Escriba la ip del servidor</property>
    <property name="type_hint">normal</property>
    <property name="has_separator">False</property>
    <child internal-child="vbox">
      <object class="GtkVBox" id="dialog-vbox1">
        <property name="visible">True</property>
        <child>
          <object class="GtkHBox" id="hbox1">
            <property name="visible">True</property>
            <child>
              <object class="GtkEntry" id="p1">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="max_length">3</property>
                <property name="invisible_char">&#x2022;</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel" id="label1">
                <property name="visible">True</property>
                <property name="label" translatable="yes">.</property>
              </object>
              <packing>
                <property name="position">1</property>
              </packing>
            </child>
            <child>
              <object class="GtkEntry" id="p2">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="max_length">3</property>
                <property name="invisible_char">&#x2022;</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="position">2</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel" id="label2">
                <property name="visible">True</property>
                <property name="label" translatable="yes">.</property>
              </object>
              <packing>
                <property name="position">3</property>
              </packing>
            </child>
            <child>
              <object class="GtkEntry" id="p3">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="max_length">3</property>
                <property name="invisible_char">&#x2022;</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="position">4</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel" id="label3">
                <property name="visible">True</property>
                <property name="label" translatable="yes">.</property>
              </object>
              <packing>
                <property name="position">5</property>
              </packing>
            </child>
            <child>
              <object class="GtkEntry" id="p4">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="invisible_char">&#x2022;</property>
              </object>
              <packing>
                <property name="position">6</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="position">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkHBox" id="hbox2">
            <property name="visible">True</property>
            <child>
              <object class="GtkLabel" id="port">
                <property name="visible">True</property>
                <property name="label" translatable="yes">Puerto: </property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkEntry" id="port_entry">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="invisible_char">&#x2022;</property>
              </object>
              <packing>
                <property name="position">1</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="position">2</property>
          </packing>
        </child>
        <child internal-child="action_area">
          <object class="GtkHButtonBox" id="dialog-action_area1">
            <property name="visible">True</property>
            <property name="layout_style">end</property>
            <child>
              <object class="GtkButton" id="button2">
                <property name="label">gtk-cancel</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="use_stock">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkButton" id="button1">
                <property name="label">gtk-ok</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="use_stock">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="position">1</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="pack_type">end</property>
            <property name="position">0</property>
          </packing>
        </child>
      </object>
    </child>
    <action-widgets>
      <action-widget response="0">button2</action-widget>
      <action-widget response="1">button1</action-widget>
    </action-widgets>
  </object>
</interface>
