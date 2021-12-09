import multiprocessing as mp
#--------------------------------------------------------------------------------#
#------------------------------gera_hash_imoveis.py------------------------------#   
#--------------------------------------------------------------------------------#

# Permitir que delete arquivos de imagens repetidas dentro de um imovel? 
# Ao desativar esta opção, apenas sera feito o calculo das hash para cada imagem
DELETE = True

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
N_PROCESSOS = mp.cpu_count()//4 