import UserForm from "./UserForm";
import { useUserForm } from "./useUserForm";

export default function UserCreate() {
  const { formData, errors, handleChange, validate } = useUserForm();

  const handleSubmit = (data) => {
    console.log("Enviar al backend:", data);
  };

  return (
    <UserForm
      formData={formData}
      errors={errors}
      handleChange={handleChange}
      validate={validate}
      onSubmit={handleSubmit}
    />
  );
}
