#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define BUFFER_SIZE 1024

void error_handling(const char *message) {
    perror(message);
    exit(1);
}

int main() {
    int sock;
    struct sockaddr_in addr1, addr2;
    char buffer[BUFFER_SIZE];
    int porta1, porta2;
    char host[] = "127.0.0.1"; // Usando "127.0.0.1" ao invés de "localhost"
    socklen_t addr_size;

    // Entrada das portas
    printf("Digite a porta: ");
    scanf("%d", &porta1);
    printf("Digite a porta do proximo: ");
    scanf("%d", &porta2);

    // Criação do socket UDP
    if ((sock = socket(PF_INET, SOCK_DGRAM, 0)) < 0)
        error_handling("socket() error");

    memset(&addr1, 0, sizeof(addr1));
    addr1.sin_family = AF_INET;
    addr1.sin_addr.s_addr = inet_addr(host);
    addr1.sin_port = htons(porta1);

    if (bind(sock, (struct sockaddr *)&addr1, sizeof(addr1)) < 0)
        error_handling("bind() error");

    memset(&addr2, 0, sizeof(addr2));
    addr2.sin_family = AF_INET;
    addr2.sin_addr.s_addr = inet_addr(host);
    addr2.sin_port = htons(porta2);

    // Enviar uma mensagem inicial para o próximo jogador
    if (porta1 == 5001) {
        printf("Jogador, insira uma mensagem para o próximo jogador: ");
        getchar(); // Consumir o caractere de nova linha deixado pelo scanf
        fgets(buffer, BUFFER_SIZE, stdin);
        buffer[strcspn(buffer, "\n")] = 0; // Remover o caractere de nova linha

        int sent = 0;
        while (!sent) {
            if (sendto(sock, buffer, strlen(buffer), 0, (struct sockaddr *)&addr2, sizeof(addr2)) == -1) {
                perror("sendto() error");
                sleep(1);
            } else {
                sent = 1;
            }
        }
        printf("Mensagem enviada para o próximo jogador.\n");
    }

    // Loop principal
    while (1) {
        addr_size = sizeof(addr2);
        int str_len = recvfrom(sock, buffer, BUFFER_SIZE - 1, 0, (struct sockaddr *)&addr2, &addr_size);
        if (str_len == -1)
            error_handling("recvfrom() error");

        buffer[str_len] = 0; // Terminar a string recebida
        printf("%s diz: %s\n", inet_ntoa(addr2.sin_addr), buffer);

        if (strcmp(buffer, "Encerrar") == 0)
            break;

        // Enviar a mensagem de volta para o próximo jogador
        printf("Digite uma mensagem: ");
        fgets(buffer, BUFFER_SIZE, stdin);
        buffer[strcspn(buffer, "\n")] = 0; // Remover o caractere de nova linha

        if (sendto(sock, buffer, strlen(buffer), 0, (struct sockaddr *)&addr2, sizeof(addr2)) == -1)
            error_handling("sendto() error");
    }

    close(sock);
    return 0;
}
