package util;

public class XmlParser {
    public static String getTagValue(String xml, String tagName) {
        try {
            String openTag = "<" + tagName + ">";
            String closeTag = "</" + tagName + ">";
            int start = xml.indexOf(openTag) + openTag.length();
            int end = xml.indexOf(closeTag);
            
            if (start < openTag.length() || end == -1) return "Erro ao extrair tag: " + tagName;
            return xml.substring(start, end).trim();
        } catch (Exception e) {
            return "";
        }
    }
}
