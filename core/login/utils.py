def valida_cpf(cpf):
    # Remove caracteres indesejados do CPF
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica se o CPF possui 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Calcula o primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    digito1 = 0 if resto == 10 or resto == 11 else resto

    # Calcula o segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    digito2 = 0 if resto == 10 or resto == 11 else resto

    # Verifica se os dígitos calculados correspondem aos dígitos informados
    return cpf[-2:] == f"{digito1}{digito2}"