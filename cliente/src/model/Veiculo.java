package model;

public class Veiculo {
    private int id;
    private String tipo;
    private String marca;
    private String modelo;
    private int ano;
    private double preco;

    public Veiculo() {}

    public Veiculo(int id, String tipo, String marca, String modelo, int ano, double preco) {
        this.id = id;
        this.tipo = tipo;
        this.marca = marca;
        this.modelo = modelo;
        this.ano = ano;
        this.preco = preco;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    
    public String getTipo() { return tipo; }
    public void setTipo(String tipo) { this.tipo = tipo; }
    
    public String getMarca() { return marca; }
    public void setMarca(String marca) { this.marca = marca; }
    
    public String getModelo() { return modelo; }
    public void setModelo(String modelo) { this.modelo = modelo; }
    
    public int getAno() { return ano; }
    public void setAno(int ano) { this.ano = ano; }
    
    public double getPreco() { return preco; }
    public void setPreco(double preco) { this.preco = preco; }

    @Override
    public String toString() {
        return "Veículo: " + marca + " " + modelo + " (" + ano + ") - R$ " + preco;
    }
}

