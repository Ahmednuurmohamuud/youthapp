import os
import django
import io
from django.core.management import call_command

# Haddii mashruucaaga uu ku jiro folder gooni ah, hubi inaad dhigto path sax ah
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youthplatform.settings')
django.setup()

with io.open("data.json", "w", encoding="utf-8") as f:
    call_command("dumpdata", indent=2, stdout=f)

print("data.json waa la abuuray!")
