#!/usr/bin/env python3
from colorama import init, Fore, Style
import os, sys, zipfile, shutil, subprocess
from pyfiglet import Figlet

comp = ['src', 'index.html',  'package.json', 'package-lock.json', 'node_modules']
so=os.name
# colores #
GREEN=f"{Fore.GREEN}{Style.BRIGHT}"
YELLOW=f"{Fore.YELLOW}{Style.BRIGHT}"
WHITE=f"{Fore.WHITE}{Style.BRIGHT}"
#

input_css = os.path.join('.', 'src', 'input.css')
output_css = os.path.join('.', 'src', 'output.css')

home_path = os.path.expanduser("~")
tw='.tw'
DIR_TW=os.path.join(home_path, tw)

def createFolder(folderName):
 if not os.path.exists(folderName):
  os.makedirs(folderName)

def indexGen():
 with open('index.html', 'w') as f:
  f.write('''
   <!doctype html>
   <html>
   <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <link href="./src/output.css" rel="stylesheet">
   </head>
   <body class="text-white">
        <div class="h-screen bg-blue-500 flex justify-center items-center">
          <h2 class="text-4xl font-bold">Ejecutando TailwindCSS con exito</h2>
        </div>
      </body>
   </html>
  ''')
  f.close()


def clearTerminal():
 if so == 'nt':
  os.system('cls')
 else:
  os.system('clear')

def ans():
 opt=input(f"{GREEN}[*]{WHITE} Deseas instalarlo en el proyecto ? [y/n]? : {GREEN}")
 if opt == 'y':
  project()
 else:
  print("Hasta la proxima instalacion...")
  sys.exit()


def help():
 print(f"""\n{YELLOW} Opciones:
 install {WHITE}: Instalar tailwindcss en el equipo
 {YELLOW}project {WHITE}: Instalar tailwindcss en el proyecto
 {YELLOW}remove {WHITE}: Eliminar todas las dependencias
 {YELLOW}delete {WHITE}: Eliminar dependencias del proyecto
 {YELLOW}execute{WHITE} : Ejecutar tailwindcss en proyecto
 {YELLOW}list{WHITE}: Listar CDN para usar en el index.html 
 {YELLOW}restore_modules{WHITE}: restaura node_modules 
 """)

def delete(comp):
 [shutil.rmtree(item) if os.path.isdir(item) else os.remove(item) for item in comp if os.path.exists(item)]

def del0(name):
 if os.path.exists(name):
  try:
   os.remove(name)
   print(f"{YELLOW}[+]{WHITE} Fichero ({name}) eliminado")
  except:
   shutil.rmtree(name)
   print(f"{YELLOW}[+]{WHITE} Directorio ({name}) eliminado")

def zip(zipName):
 with zipfile.ZipFile(zipName, 'w') as zipf:
  for item in comp:
   if os.path.isdir(item):
    for root, _, files in os.walk(item):
     for file in files:
      file_path = os.path.join(root, file)
      arcname = os.path.relpath(file_path, os.path.dirname(item))
      zipf.write(file_path, arcname)
   else:
    zipf.write(item)
 delete(comp)
 if os.path.exists(DIR_TW):
  shutil.rmtree(DIR_TW)
 createFolder(DIR_TW)
 print(f"{GREEN}[+]{WHITE} Guardando dependencias en [HOME]")
 shutil.move(zipName, DIR_TW)
 print(f"{GREEN}[+]{WHITE} Guardado exitsamente...")
 ans()

def execute(command):
 if so == 'nt':
  os.system(f'{command} >nul 2>nul')
 else:
  os.system(f'{command} 2>/dev/null >/dev/null')

def install():
 print(f"{GREEN}[+]{WHITE} Generando [{GREEN}package.json{WHITE}]")
 execute('npm init -y')
 print(f"{GREEN}[+]{WHITE} Fichero generado con exito...")
 print(f'{GREEN}[+]{WHITE} Generando directorio [{GREEN}src{WHITE}]')
 createFolder('src')
 fileCSS=os.path.join('.', 'src', 'input.css')
 print(f"{GREEN}[+]{WHITE} Generando archivo [{GREEN}input.css{WHITE}]")
 with open(fileCSS, 'w') as f:
  f.write('@import "tailwindcss";')
  f.close()
 indexGen()
 print(f"{GREEN}[+]{WHITE} Fichero de estilo generado con exito")
 print(f"{GREEN}[+]{WHITE} Instalando dependencias...")
 execute('npm install tailwindcss @tailwindcss/cli')
 print(f'{GREEN}[+]{WHITE} Comprimiendo dependencias ...') ; zip('install.zip')

def project():
 try:
  print(f"{GREEN}[+]{WHITE} Extrayendo dependencias...")
  zip_path = os.path.join(DIR_TW, 'install.zip')
  zipfile.ZipFile(zip_path).extractall(os.getcwd())
  print(f'{GREEN}[+]{WHITE} Ejecutando NPX ahora')
  print(f"{GREEN}[+]{WHITE} No cierre esta ventana...")
  os.system(f'npx tailwindcss -i {input_css} -o {output_css} --watch')
 except:
  install()


def restore_modules():
 modules = os.path.join(os.getcwd(), 'node_modules')
 if os.path.exists(modules):
  shutil.rmtree(modules)
 zip_path = os.path.join(DIR_TW, "install.zip")
 extract_dir = os.getcwd()
 with zipfile.ZipFile(zip_path, 'r') as zip_ref:
  for file in zip_ref.namelist():
   if file.startswith("node_modules/"):
    zip_ref.extract(file, extract_dir)
    print(f"Extrayendo: {file}")
 

listCDN=f'''
https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4
https://cdn.tailwindcss.com/3.4.16
https://cdn.tailwindcss.com/3.4.9
https://cdn.tailwindcss.com/3.4.8
https://cdn.tailwindcss.com/3.4.7
https://cdn.tailwindcss.com/3.3.1
https://cdn.tailwindcss.com/3.0.4
'''

def selOption(opc):
 if opc == 'install':
  print(f'Instalando TailwindCSS en {GREEN}HOME{WHITE}') ; install()
 elif opc == 'project':
  project()
 elif opc == 'remove':
  try:
   shutil.rmtree(os.path.join(DIR_TW))
  except:
   pass
  print(f'{GREEN}[+]{WHITE} Todas las dependencias desinstaladas del equipo')
 elif opc == 'delete':
  for i in comp:
   del0(i)
 elif opc == 'execute':
  os.system(f'npx tailwindcss -i {input_css} -o {output_css} --watch')
 elif opc == 'list':
  print(listCDN)
 elif opc == "restore_modules":
  restore_modules()
 else:
  print("Opcion Invalida...")

def start():
 clearTerminal()
 print(WHITE + Figlet(font='small').renderText("TwInstaller"))
 opc=sys.argv
 if len(opc) == 2:
  selOption(opc[1])
 else:
  print(" Comandos de (ayuda)")
  help()

if __name__ == '__main__':
 try:
  start()
 except KeyboardInterrupt:
  print("[+] Script Interrumpido con [CTRL+C]")
