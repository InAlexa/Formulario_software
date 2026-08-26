import UserForm from "./components/UserForm";
import { useUserForm } from "./hooks/useClientForm";
function App() {
  const { formData, errors, handleChange, validate } = useUserForm();

  const handleSubmit = (data) => {
    console.log("Datos del formulario:", data);
  };

  return (
    <main
      style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
    >
      <h1>Crear usuario</h1>

      <UserForm
        formData={formData}
        errors={errors}
        handleChange={handleChange}
        validate={validate}
        onSubmit={handleSubmit}
      />
    </main>
  );
}

export default App;
