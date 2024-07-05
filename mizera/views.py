from django.shortcuts import render, redirect
import json, re
from .models import NumeroTelefone, Relatorio
from django.http import JsonResponse



def buscar_numero_telefone(request):
    if request.method == 'GET' and 'termo' in request.GET:
        termo_pesquisa = request.GET['termo']
        # Fazer a consulta no banco de dados para buscar números de telefone semelhantes
        resultados = NumeroTelefone.objects.filter(numero__icontains=termo_pesquisa)[:10]  # Limitar a 10 resultados
        numeros = [{'numero': numero.numero} for numero in resultados]
        return JsonResponse(numeros, safe=False)
    else:
        return JsonResponse({'error': 'Requisição inválida'}, status=400)

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
