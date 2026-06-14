import service.SoapClient;
import util.XmlParser;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        SoapClient client = new SoapClient();
        
        while (true) {
            System.out.println("\n--- CONCESSIONÁRIA (SOAP) ---");
            System.out.println("1. Listar | 2. Inserir | 3. Simular | 4. Excluir | 0. Sair");
            String op = scanner.nextLine();
            
            try {
                if (op.equals("0")) break;
                
                switch (op) {
                    case "1":
                        String resList = client.enviarRequisicao("listar_veiculos", "");
                        
                        String conteudoResposta = XmlParser.getTagValue(resList, "listar_veiculosResponse");
                        String listaVeiculos = XmlParser.getTagValue(conteudoResposta, "result");

                        if (listaVeiculos.contains("Erro ao extrair")) {
                            System.out.println("Erro ao listar veículos: " + listaVeiculos);
                        } else {
                            java.util.regex.Pattern p = java.util.regex.Pattern.compile("<item>(.*?)</item>", java.util.regex.Pattern.DOTALL);
                            java.util.regex.Matcher m = p.matcher(listaVeiculos);

                            System.out.println("\n--- LISTA DE VEÍCULOS ---");
                            System.out.printf("%-5s | %-10s | %-10s | %-15s | %-5s | %-10s%n", "ID", "TIPO", "MARCA", "MODELO", "ANO", "PREÇO");
                            System.out.println("--------------------------------------------------------------------------");

                            while (m.find()) {
                                String conteudo = m.group(1); 
                                
                                String id = XmlParser.getTagValue(conteudo, "id");
                                String tipo = XmlParser.getTagValue(conteudo, "tipo");
                                String marca = XmlParser.getTagValue(conteudo, "marca");
                                String modelo = XmlParser.getTagValue(conteudo, "modelo");
                                String ano = XmlParser.getTagValue(conteudo, "ano");
                                String preco = XmlParser.getTagValue(conteudo, "preco");

                                System.out.printf("%-5s | %-10s | %-10s | %-15s | %-5s | %-10s%n", id, tipo, marca, modelo, ano, preco);
                            }
                        }
                        break;

                    case "2":
                        System.out.print("Tipo, Marca, Modelo, Ano, Preco (sep. por enter): ");
                        String body = "<tipo>"+scanner.nextLine()+"</tipo><marca>"+scanner.nextLine()+"</marca>" +
                                    "<modelo>"+scanner.nextLine()+"</modelo><ano>"+scanner.nextLine()+"</ano>" +
                                    "<preco>"+scanner.nextLine()+"</preco>";
                        
                        String respostaBruta = client.enviarRequisicao("inserir_veiculo", body);
                        
                        System.out.println("\n--- RESPOSTA DO SERVIDOR ---");
                        System.out.println(XmlParser.formatarXml(respostaBruta));
                        break;
                    case "3":
                        System.out.print("ID: ");
                        String idVeic = scanner.nextLine();
                        System.out.print("Entrada: ");
                        String valorEntrada = scanner.nextLine(); 
                        System.out.print("Parcelas: ");
                        String numParcelas = scanner.nextLine();

                        String bSim = "<veiculo_id>" + idVeic + "</veiculo_id>" +
                                    "<valor_entrada>" + valorEntrada + "</valor_entrada>" +
                                    "<parcelas>" + numParcelas + "</parcelas>";
                        
                        String resSim = client.enviarRequisicao("simular_financiamento", bSim);
                        
                        String vParc = XmlParser.getTagValue(resSim, "valor_parcela");
                        String totParc = XmlParser.getTagValue(resSim, "total_apenas_parcelas");
                        String totFinal = XmlParser.getTagValue(resSim, "total_final");
                        String nParc = XmlParser.getTagValue(resSim, "num_parcelas");
                        
                        System.out.println("\n--- RESULTADO DA SIMULAÇÃO ---");
                        System.out.println("Plano: " + nParc + "x de R$ " + vParc);
                        System.out.println("----------------------------------------------");
                        System.out.println("Soma das parcelas:    R$ " + totParc);
                        System.out.println("Valor da entrada:     R$ " + valorEntrada); 
                        System.out.println("CUSTO TOTAL (FINAL):  R$ " + totFinal);
                        System.out.println("----------------------------------------------");
                        break;

                    case "4":
                        System.out.print("ID a excluir: ");
                        String idParaExcluir = scanner.nextLine();
                        
                        String resExcluir = client.enviarRequisicao("excluir_veiculo", "<id>" + idParaExcluir + "</id>");
                        
                        System.out.println("\n--- RESPOSTA DA EXCLUSÃO ---");
                        System.out.println(XmlParser.formatarXml(resExcluir));
                        
                        String sucesso = XmlParser.getTagValue(resExcluir, "result");
                        if ("true".equals(sucesso)) {
                            System.out.println("\nStatus: Veículo excluído com sucesso!");
                        } else {
                            System.out.println("\nStatus: Falha ao excluir o veículo (ou ID inexistente).");
                        }
                        break;
                }
            } catch (Exception e) {
                System.out.println("Erro: " + e.getMessage());
            }
        }
    }
}
