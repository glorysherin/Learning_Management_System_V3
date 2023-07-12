from django.shortcuts import render
from subprocess import Popen, PIPE

def compiler_view(request):
    if request.method == 'POST':
        code = request.POST.get('code', '')
        language = request.POST.get('language', '')
        input_value = request.POST.get('input_value', '')
        result = compile_and_execute(code, language, input_value)

        return render(request, 'compiler/compiler.html', {'code': code, 'result': result,'language':language})
    else:
        return render(request, 'compiler/compiler.html')

def compile_and_execute(code, language, input_value):
    if language == 'python':
        process = Popen(['python', '-c', code], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    elif language == 'java':
        process = Popen(['java', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    elif language == 'c':
        process = Popen(['gcc', '-xc', '-o', 'myprogram', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    elif language == 'html' or language == 'tailwind' or language == 'bootstrap':
        return f"<frame>{code}</frame>"
    elif language == 'js':
        try:
            compiled_output = eval(code)
            return compiled_output
        except Exception as e:
            return f"Error: {str(e)}"
    else:
        return 'Unsupported language'

    stdout, stderr = process.communicate(input=input_value.encode('utf-8'))

    if stderr:
        result = stderr.decode('utf-8')
    else:
        result = stdout.decode('utf-8')

    return result