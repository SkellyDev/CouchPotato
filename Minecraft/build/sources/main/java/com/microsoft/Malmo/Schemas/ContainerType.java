//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.4 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2020.10.31 at 07:07:04 PM PDT 
//


package com.microsoft.Malmo.Schemas;

import javax.xml.bind.annotation.XmlEnum;
import javax.xml.bind.annotation.XmlEnumValue;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for ContainerType.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * <p>
 * <pre>
 * &lt;simpleType name="ContainerType">
 *   &lt;restriction base="{http://www.w3.org/2001/XMLSchema}string">
 *     &lt;enumeration value="dispenser"/>
 *     &lt;enumeration value="chest"/>
 *     &lt;enumeration value="trapped_chest"/>
 *     &lt;enumeration value="hopper"/>
 *     &lt;enumeration value="dropper"/>
 *     &lt;enumeration value="white_shulker_box"/>
 *     &lt;enumeration value="orange_shulker_box"/>
 *     &lt;enumeration value="magenta_shulker_box"/>
 *     &lt;enumeration value="light_blue_shulker_box"/>
 *     &lt;enumeration value="yellow_shulker_box"/>
 *     &lt;enumeration value="lime_shulker_box"/>
 *     &lt;enumeration value="pink_shulker_box"/>
 *     &lt;enumeration value="gray_shulker_box"/>
 *     &lt;enumeration value="silver_shulker_box"/>
 *     &lt;enumeration value="cyan_shulker_box"/>
 *     &lt;enumeration value="purple_shulker_box"/>
 *     &lt;enumeration value="blue_shulker_box"/>
 *     &lt;enumeration value="brown_shulker_box"/>
 *     &lt;enumeration value="green_shulker_box"/>
 *     &lt;enumeration value="red_shulker_box"/>
 *     &lt;enumeration value="black_shulker_box"/>
 *   &lt;/restriction>
 * &lt;/simpleType>
 * </pre>
 * 
 */
@XmlType(name = "ContainerType")
@XmlEnum
public enum ContainerType {

    @XmlEnumValue("dispenser")
    DISPENSER("dispenser"),
    @XmlEnumValue("chest")
    CHEST("chest"),
    @XmlEnumValue("trapped_chest")
    TRAPPED_CHEST("trapped_chest"),
    @XmlEnumValue("hopper")
    HOPPER("hopper"),
    @XmlEnumValue("dropper")
    DROPPER("dropper"),
    @XmlEnumValue("white_shulker_box")
    WHITE_SHULKER_BOX("white_shulker_box"),
    @XmlEnumValue("orange_shulker_box")
    ORANGE_SHULKER_BOX("orange_shulker_box"),
    @XmlEnumValue("magenta_shulker_box")
    MAGENTA_SHULKER_BOX("magenta_shulker_box"),
    @XmlEnumValue("light_blue_shulker_box")
    LIGHT_BLUE_SHULKER_BOX("light_blue_shulker_box"),
    @XmlEnumValue("yellow_shulker_box")
    YELLOW_SHULKER_BOX("yellow_shulker_box"),
    @XmlEnumValue("lime_shulker_box")
    LIME_SHULKER_BOX("lime_shulker_box"),
    @XmlEnumValue("pink_shulker_box")
    PINK_SHULKER_BOX("pink_shulker_box"),
    @XmlEnumValue("gray_shulker_box")
    GRAY_SHULKER_BOX("gray_shulker_box"),
    @XmlEnumValue("silver_shulker_box")
    SILVER_SHULKER_BOX("silver_shulker_box"),
    @XmlEnumValue("cyan_shulker_box")
    CYAN_SHULKER_BOX("cyan_shulker_box"),
    @XmlEnumValue("purple_shulker_box")
    PURPLE_SHULKER_BOX("purple_shulker_box"),
    @XmlEnumValue("blue_shulker_box")
    BLUE_SHULKER_BOX("blue_shulker_box"),
    @XmlEnumValue("brown_shulker_box")
    BROWN_SHULKER_BOX("brown_shulker_box"),
    @XmlEnumValue("green_shulker_box")
    GREEN_SHULKER_BOX("green_shulker_box"),
    @XmlEnumValue("red_shulker_box")
    RED_SHULKER_BOX("red_shulker_box"),
    @XmlEnumValue("black_shulker_box")
    BLACK_SHULKER_BOX("black_shulker_box");
    private final String value;

    ContainerType(String v) {
        value = v;
    }

    public String value() {
        return value;
    }

    public static ContainerType fromValue(String v) {
        for (ContainerType c: ContainerType.values()) {
            if (c.value.equals(v)) {
                return c;
            }
        }
        throw new IllegalArgumentException(v);
    }

}
