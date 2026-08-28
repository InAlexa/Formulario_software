import RegistroForm from "./features/registro/components/RegistroForm";
import VerificacionCorreo from "./features/registro/components/VerificacionCorreo";

function App() {
  const esVerificacion = window.location.pathname === "/verificado";

  return esVerificacion ? <VerificacionCorreo /> : <RegistroForm />;
}

export default App;
