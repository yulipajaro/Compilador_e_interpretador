from django.shortcuts import render
from MiSalud import Home;


resultado = str();
dic = {};

# Create your views here.
def Inicio(request):
    global dic
    resultado = "";

    if(request.method=='POST'):
        
        cadena = request.POST['cadena'];
        
        resultado = Home.Funcion_Main(cadena);
        print(resultado.replace('None',''));
        #dic = {"dic":resultado}
        return render(request, "index.html", {"dic":resultado});
       
    return render(request, "index.html");
