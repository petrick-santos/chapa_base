## CHAPA BASE
Esse software é uma ferramenta desenvolvida como parte do Trabalho de Conclusão do Curso de Engenharia Civil da Universidade Federal do Rio Grande do Sul, do aluno Petrick Eichwald Rosa dos Santos. O projeto foi realizado sob a orientação
do professor Enio Carlos Mesacasa Júnior, que atuou como orientador durante todo o desenvolvimento do software.

O objetivo deste programa é auxiliar no cálculo das principais dimensões de ligações de chapas de base de pilares metálicos, proporcionando uma solução prática para estudantes, engenheiros e profissionais da área.

### - Funcionalidades
O software é capaz de calcular as dimensões dos principais elementos que compõem as ligações de base de pilares, com suas limitações, para diferentes combinações de solicitações.

#### Dos elementos que estão englobados no software:
- Largura, comprimento e espessuras das **chapas de base**.
- Diâmetro e embutimento dos **chumbadores**.
- Áreas das **bases de concreto**.

#### Das limitações do software:
- Solicitações de tração sem momentos, compressão com/sem momentos e cortante pode existir em todos os casos.
- Número de chumbadores de 4 à 10 por ligação.
- O cisalhamento é a absorvido apenas por 2 chumbadores, conforme recomendações.
- Material dos chumbadores - F1554 grau 36, 55 e 105 (Recomenda-se adoção do grau 36).
- Chumbadores pré-instalados.
- A resistência da placa ao cisalhamento não foi verificada.
- Não abordadas ligações com enrijecedores.

  **Para maior autonomia no dimensionamento das ligações acrescentou-se no software a opção de verificação de ligações, permitindo que os usuários verifiquem configurações alternativas das ligações dimensionadas, porém deve-se atentar para a possibilidade de resultados incoerentes, uma vez que o software permitirá   entradas de valores que podem não estar regidas pelos métodos de dimensionamento. Exemplo: Chumbadores posicionados exatamente sob a alma ou mesas dos perfis.** 

### - Requesitos do sistema
Desenvolvido para sistema operacional Windows.

### - Instalação
Não requer instalação, basta baixar o executável **chapa_base.exe** e executar como administrador.

### - Interface
![interface_tcc](https://github.com/petrick-santos/chapa_base/assets/127921718/81ab3296-2df2-441d-b845-91fd3899008d)

O objetivo é que a interface seja intuitiva e rápida de usar, precisando apenas das entradas necessárias para o dimensionamento/verificação das ligaçoes.

As informações de cada elemento estão separadas por frames, de modo a evitar confusão.
O frame de **memorial** exibirá os resultados parciais que fazem parte do dimensionamento as ligações, de modo a facilitar a verificação dos resultados. Sendo possível salva-los em .txt para futuras observações.

### - Licença
Com o intuito de promover a colaboração entre a comunidade de projetos de estruturas de aço, o software tem a sua liceça pública, permitindo que a comunidade continue o desenvolvimento do programa futuramente.

### - Contato
Em caso de dúvidas meu e-mail para contato é:
petrick_@hotmail.com

### - Agradecimento
um agradecimento especial para meu orientador, Enio, que disponibilizou seu tempo e conhecimento os quais tornaram possível a realização desse software, muito obrigado.

### - Observações
Vale ressaltar que os software desenvolvido foi o primeiro contato do estudante com a linguagem de programação python, logo, futuros programadores que venham alterar os software é preciso que tenham ciência que os algoritmos podem não ter sido concebidos da forma mais otimizada.
















































