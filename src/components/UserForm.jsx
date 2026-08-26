import styles from "./UserForm.module.css";

export default function UserForm({
  formData,
  errors,
  handleChange,
  validate,
  onSubmit,
}) {
  const handleSubmit = (e) => {
    e.preventDefault();

    if (validate()) {
      onSubmit(formData);
    }
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <div className={styles.field}>
        <label htmlFor="email">Correo</label>
        <input
          id="email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          className={errors.email ? styles.inputError : ""}
          placeholder="correo@ejemplo.com"
        />
        {errors.email && <span className={styles.error}>{errors.email}</span>}
      </div>

      <div className={styles.row}>
        <div className={styles.field}>
          <label htmlFor="first_name">Nombre</label>
          <input
            id="first_name"
            name="first_name"
            type="text"
            value={formData.first_name}
            onChange={handleChange}
            className={errors.first_name ? styles.inputError : ""}
            placeholder="Juan"
          />
          {errors.first_name && (
            <span className={styles.error}>{errors.first_name}</span>
          )}
        </div>

        <div className={styles.field}>
          <label htmlFor="last_name">Apellidos</label>
          <input
            id="last_name"
            name="last_name"
            type="text"
            value={formData.last_name}
            onChange={handleChange}
            className={errors.last_name ? styles.inputError : ""}
            placeholder="Pérez López"
          />
          {errors.last_name && (
            <span className={styles.error}>{errors.last_name}</span>
          )}
        </div>
      </div>

      <div className={styles.row}>
        <div className={styles.field}>
          <label htmlFor="age">Edad</label>
          <input
            id="age"
            name="age"
            type="number"
            min="1"
            value={formData.age}
            onChange={handleChange}
            className={errors.age ? styles.inputError : ""}
            placeholder="25"
          />
          {errors.age && <span className={styles.error}>{errors.age}</span>}
        </div>

        <div className={styles.field}>
          <label htmlFor="password">Contraseña</label>
          <input
            id="password"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            className={errors.password ? styles.inputError : ""}
            placeholder="••••••••"
          />
          {errors.password && (
            <span className={styles.error}>{errors.password}</span>
          )}
        </div>
      </div>

      <button type="submit" className={styles.submit}>
        Guardar usuario
      </button>
    </form>
  );
}
