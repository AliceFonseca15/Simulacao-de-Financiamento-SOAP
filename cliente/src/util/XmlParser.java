package util;
import javax.xml.transform.*;
import javax.xml.transform.stream.*;
import java.io.*;
public class XmlParser {
    public static String getTagValue(String xml, String tagName) {
        try {
            String regex = "<[^/>]*:?" + tagName + "[^>]*>(.*?)</[^>]*:?" + tagName + ">";
            java.util.regex.Pattern pattern = java.util.regex.Pattern.compile(regex, java.util.regex.Pattern.DOTALL);
            java.util.regex.Matcher matcher = pattern.matcher(xml);

            if (matcher.find()) {
                return matcher.group(1).trim();
            }
            return "Erro ao extrair tag: " + tagName;
        } catch (Exception e) {
            return "Erro: " + e.getMessage();
            }
        }

    public static String formatarXml(String xml) {
        try {
            Source xmlInput = new StreamSource(new StringReader(xml));
            StringWriter stringWriter = new StringWriter();
            Transformer transformer = TransformerFactory.newInstance().newTransformer();
            
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
            
            transformer.transform(xmlInput, new StreamResult(stringWriter));
            return stringWriter.toString();
        } catch (Exception e) {
            return xml; 
        }
    }  
} 