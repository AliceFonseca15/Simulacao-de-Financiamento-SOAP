package service;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;

public class SoapClient {
    private static final String ENDPOINT = "http://localhost:8000/";

    public String enviarRequisicao(String metodo, String bodyContent) throws Exception {
        String soapEnvelope = 
            "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:con=\"concessionaria.soap\">" +
            "   <soapenv:Body>" +
            "      <con:" + metodo + ">" + bodyContent + "</con:" + metodo + ">" +
            "   </soapenv:Body>" +
            "</soapenv:Envelope>";

        URL url = new URL(ENDPOINT);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "text/xml; charset=utf-8");
        conn.setRequestProperty("SOAPAction", metodo);
        conn.setDoOutput(true);

        try (OutputStream os = conn.getOutputStream()) {
            os.write(soapEnvelope.getBytes(StandardCharsets.UTF_8));
        }

        int responseCode = conn.getResponseCode();
        InputStream is = (responseCode >= 200 && responseCode < 300) ? conn.getInputStream() : conn.getErrorStream();

        try (BufferedReader br = new BufferedReader(new InputStreamReader(is, StandardCharsets.UTF_8))) {
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) response.append(line.trim());
            return response.toString();
        }
    }
}
