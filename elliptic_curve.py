!pip install tinyec
import ssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from tinyec import registry

def get_curve_parameters(hostname, port=443):
    print(f"--- Fetching Certificate from {hostname} ---")

    try:
        pem_data = ssl.get_server_certificate((hostname, port))
        cert = x509.load_pem_x509_certificate(pem_data.encode(), default_backend())
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    # Extract Public Key
    public_key = cert.public_key()

    if isinstance(public_key, ec.EllipticCurvePublicKey):
        # Get Curve Name
        curve_name = public_key.curve.name
        print(f"Curve Found: {curve_name}")

        try:
            curve = registry.get_curve(curve_name)
            print("\n[+] Extracted Field Characteristics:")
            print(f"    p = {curve.field.p}")
            print(f"    a = {curve.a}")
            print(f"    b = {curve.b}")
            print(f"\n[+] Equation: y^2 = x^3 + {curve.a}x + {curve.b} (mod {curve.field.p})")
        except LookupError:
            print(f"Details for '{curve_name}' not in tinyec registry.")
    else:
        print("Not an Elliptic Curve certificate.")


get_curve_parameters("www.youtube.com")
