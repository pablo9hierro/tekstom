from django.shortcuts import render, redirect
import json, re
from mizera.models import NumeroTelefone, Relatorio
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import Q


def relatorio(request, numero):
    numero_telefone = get_object_or_404(NumeroTelefone, numero=numero)
    apelido = numero_telefone.relatorio_set.first().apelido if numero_telefone.relatorio_set.exists() else ''
    context = {
        'numero': numero_telefone.numero,
        'apelido': apelido
    }
    return render(request, 'relatorio.html', context)

def relatorio_numero(request, numero):
    
    return render(request, 'relatorio.html', {'numero': numero})

def todosforms(request):
    # Buscar todos os relatórios
    relatorios = Relatorio.objects.all()

    # Renderizar o template com os dados dos relatórios
    return render(request, 'todosforms.html', {'relatorios': relatorios})


@csrf_exempt
def salvar_relatorio(request):
    if request.method == 'POST':
        try:
            # Obtenha os dados do formulário
            numero = request.POST.get('numero_telefone')
            texto_livre = request.POST.get('texto_livre')
            velocidade_resposta = request.POST.get('velocidade_resposta')
            nivel_engajamento = request.POST.get('nivel_engajamento')
            comprometido = request.POST.get('comprometido', False)
            apelido = request.POST.get('apelido')

            # Verifique se os dados estão chegando corretamente
            print(f'Dados recebidos: {numero}, {texto_livre}, ...')

            # Busque ou crie o objeto NumeroTelefone pelo número
            numero_telefone, created = NumeroTelefone.get_or_create(numero)

            # Corrigir o valor de comprometido para um booleano
            if comprometido == 'true':  # Verifica se é a string 'true'
                comprometido = True
            elif comprometido == 'false':  # Verifica se é a string 'false'
                comprometido = False
            else:
                # Caso o valor não seja 'true' nem 'false', defina um valor padrão
                comprometido = False  # Ou outro valor padrão que faça sentido para o seu caso

            # Crie um novo relatório associado ao número de telefone encontrado ou criado
            relatorio = Relatorio.objects.create(
                numero_telefone=numero_telefone,
                texto_livre=texto_livre,
                velocidade_resposta=velocidade_resposta,
                nivel_engajamento=nivel_engajamento,
                comprometido=comprometido,
                apelido=apelido
            )

            return JsonResponse({'message': 'Dados enviados com sucesso'})

        except Exception as e:
            # Capture e registre o erro para debug
            print(f'Erro ao salvar relatório: {str(e)}')
            return JsonResponse({'error': 'Erro ao salvar relatório'}, status=500)

    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)

def buscar_numero_telefone(request):
    if request.method == 'GET' and 'termo' in request.GET:
        termo_pesquisa = request.GET['termo'].strip()
        
        if not termo_pesquisa:
            return JsonResponse({'error': 'Termo de pesquisa inválido'}, status=400)

        resultados = NumeroTelefone.objects.filter(
            Q(numero__icontains=termo_pesquisa) | Q(relatorio__apelido__icontains=termo_pesquisa)
        ).distinct()[:10]  # Limitar a 10 resultados
        
        numeros = [{'numero': numero.numero, 'apelido': numero.relatorio_set.first().apelido if numero.relatorio_set.exists() else ''} for numero in resultados]
        
        if numeros:
            return JsonResponse(numeros, safe=False)
        else:
            return JsonResponse({'message': 'Nenhum resultado encontrado'}, status=404)
    else:
        return JsonResponse({'error': 'Requisição inválida'}, status=400)
    
def pagina_extrato(request):
    numero_telefone = request.GET.get('numero')
    numero_telefone_obj = get_object_or_404(NumeroTelefone, numero=numero_telefone)
    relatorios = Relatorio.objects.filter(numero_telefone=numero_telefone_obj)

    return render(request, 'extrato.html', {
        'numero': numero_telefone,
        'relatorios': relatorios,
    })

def upload_json(request):
    if request.method == 'POST' and request.FILES.get('json_file'):
        json_file = request.FILES['json_file']
        
        json_content = json_file.read().decode('utf-8')

        try:
            data = json.loads(json_content)
            for item in data:
                for key, value in item.items():
                    # Verifica se o valor é um número de telefone válido
                    if value.strip().startswith('+'):
                        # Remove espaços em branco extras e adiciona ao banco de dados
                        numero_telefone = value.strip().replace(" ", "")  # Remover espaços em branco extras
                        NumeroTelefone.objects.create(numero=numero_telefone)
            
            # Após processar o JSON com sucesso, redireciona para a página dash.html
            print('Funcionou')  # Print no console indicando que funcionou
            return redirect('dash')
        
        except json.JSONDecodeError:
            # Retorna renderização de 'formulariojson.html' com mensagem de erro
            return render(request, 'formulariojson.html', {'error_message': 'Erro ao processar o JSON'})

    return render(request, 'formulariojson.html')


def dash_def(request):
    # Aqui você pode adicionar lógica para buscar e exibir dados necessários na página dash.html
    numeros_telefone = NumeroTelefone.objects.all()  # Exemplo de busca de todos os números de telefone
    context = {'numeros_telefone': numeros_telefone}
    return render(request, 'dash.html', context)
