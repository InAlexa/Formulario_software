import { useState, useEffect } from "react";

const EMPTY_FORM = {
  email: "",
  first_name: "",
  last_name: "",
  age: "",
  password: "",
};

const buildInitialForm = (user) => {
  if (!user) return EMPTY_FORM;

  return {
    email: user.email ?? "",
    first_name: user.first_name ?? "",
    last_name: user.last_name ?? "",
    age: user.age ?? "",
    password: "",
  };
};

export function useUserForm(user = null) {
  const [formData, setFormData] = useState(() => buildInitialForm(user));
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (user) {
      setFormData(buildInitialForm(user));
    }
  }, [user]);

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: null,
      }));
    }
  };

  const validate = () => {
    const newErrors = {};

    if (!formData.email.trim()) {
      newErrors.email = "El correo es requerido";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = "El correo no es válido";
    }

    if (!formData.first_name.trim()) {
      newErrors.first_name = "El nombre es requerido";
    }

    if (!formData.last_name.trim()) {
      newErrors.last_name = "Los apellidos son requeridos";
    }

    if (!formData.age) {
      newErrors.age = "La edad es requerida";
    } else if (Number(formData.age) < 1) {
      newErrors.age = "La edad debe ser válida";
    }

    if (!formData.password) {
      newErrors.password = "La contraseña es requerida";
    } else if (formData.password.length < 8) {
      newErrors.password = "La contraseña debe tener al menos 8 caracteres";
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

  const resetForm = () => {
    setFormData(buildInitialForm(user));
    setErrors({});
  };

  return {
    formData,
    errors,
    handleChange,
    validate,
    resetForm,
  };
}
