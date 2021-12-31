import multiprocessing as mp
#--------------------------------------------------------------------------------#
#-----------------------------acha_duplicadas_csv.py-----------------------------#   
#--------------------------------------------------------------------------------#
N_PROCESSOS_CSV = mp.cpu_count() //2

# Cada camada ira filtrar o csv cada vez mais, onde a camada 1 é a mais generica,
# com menos chance de ter tido erro ao gear o csv e a camada 3 é a mais especifica,
# com possiveis erros no csv. 

# Camada 1:
#  - tipo
#  - classe_energetica_id
#  - garagem
#  - terraco
#  - piscina
#  - terreno    
CAMADA1 = True
# Camada 2:
#  - 'data_public'-abp
#       ->Porcentagem abaixo e acima que podemos considerar uma area realtivamente perto uma da outra.
#       ->(1 - INTERVALO_AREA) é a menor area aceitavel 
#       ->(1 + INTERVALO_AREA) é a maior area aceitavel
CAMADA2 = True
INTERVALO_AREA = 0.25
# Camada 3: 
#     -  tipologia  
#     -  freguesia_id
#     -  regiao_id  
CAMADA3 = True



#--------------------------------------------------------------------------------#
#------------------------------gera_hash_imoveis.py------------------------------#   
#--------------------------------------------------------------------------------#

# Permitir que delete arquivos de imagens repetidas dentro de um imovel? 
# Ao desativar esta opção, apenas sera feito o calculo das hash para cada imagem
DELETE = False

#--------------------------------------------------------------------------------#
#-------------------------------compara_imoveis.py-------------------------------#   
#--------------------------------------------------------------------------------#

# Acima desse valor, duas imagens são diferentes
DHASH_MAX = 12

# Abaixo desse valor, duas imagens são iguais
DHASH_MIN = 6

# acima desse valor, dois imoveis são definitivamente iguais
PROPORCAO_IGUAIS = 0.8

# acima desse valor, dois imoveis são definitivamente diferentes
PROPORCAO_DIFERENTES = 0.8

# acima desse valor, dois imoveis são definitivamente indeterminados
PROPORCAO_INDETERMINADOS = 0.8

# Quantidade de quantidade de imagens diferentes aceitavel entre 2 imoveis
DIFERENCA_MAXIMA = 2

# Quantidade de processos em que serão divididos 
N_PROCESSOS = mp.cpu_count()//2