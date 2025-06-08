from supabase import create_client, Client

SUPABASE_URL = "https://tuproyecto.supabase.co"
SUPABASE_KEY = "tu-clave-api"

def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_asistencias():
    supabase = get_supabase_client()
    response = supabase.table("asistencias").select("*").execute()
    return response.data
