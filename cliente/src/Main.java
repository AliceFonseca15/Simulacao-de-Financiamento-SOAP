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
                        System.out.println("Dados: " + XmlParser.getTagValue(resList, "listar_veiculosResponse"));
                        break;
                    case "2":
                        System.out.print("Tipo, Marca, Modelo, Ano, Preco (sep. por enter): ");
                        String body = "<tipo>"+scanner.nextLine()+"</tipo><marca>"+scanner.nextLine()+"</marca>" +
                                      "<modelo>"+scanner.nextLine()+"</modelo><ano>"+scanner.nextLine()+"</ano>" +
                                      "<preco>"+scanner.nextLine()+"</preco>";
                        System.out.println(client.enviarRequisicao("inserir_veiculo", body));
                        break;
                    case "3":
                        System.out.print("ID, Entrada, Parcelas: ");
                        String bSim = "<veiculo_id>"+scanner.nextLine()+"</veiculo_id><valor_entrada>"+scanner.nextLine()+"</valor_entrada>" +
                                     "<parcelas>"+scanner.nextLine()+"</parcelas>";
                        String resSim = client.enviarRequisicao("simular_financiamento", bSim);
                        System.out.println("Parcela: " + XmlParser.getTagValue(resSim, "valor_parcela"));
                        break;
                    case "4":
                        System.out.print("ID a excluir: ");
                        System.out.println(client.enviarRequisicao("excluir_veiculo", "<id>"+scanner.nextLine()+"</id>"));
                        break;
                }
            } catch (Exception e) {
                System.out.println("Erro: " + e.getMessage());
            }
        }
    }
}
