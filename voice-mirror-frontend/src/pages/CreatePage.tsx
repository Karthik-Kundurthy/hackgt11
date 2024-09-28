import PersonaForm from "../components/PersonaForm";

export default function CreatePage() {
  return (
    <div className="flex flex-col justify-center items-center gap-5">
      <h1 className="text-5xl font-bold text-primaryText">Create a persona.</h1>
      <PersonaForm />
    </div>
  );
}
