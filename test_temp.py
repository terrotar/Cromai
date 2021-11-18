
import tempfile

temp = tempfile.NamedTemporaryFile()
print(temp)
print(temp.name)



"""
import tempfile

arquivoTemporario = tempfile.TemporaryFile()

arquivoTemporario.write(b'qualquer coisa')

arquivoTemporario.seek(0)

print(str(arquivoTemporario.read(), encoding='utf8'))

arquivoTemporario.close()
"""
