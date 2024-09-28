import PersonaForm from "./PersonaForm";
import { useParams } from "react-router-dom";

export default function EditPage() {
  // use this id later
  const { id } = useParams();

  return (
    <div className="flex flex-col justify-center items-center gap-5">
      <h1 className="text-5xl font-bold text-primaryText">Edit a persona.</h1>
      <PersonaForm />
    </div>
  );
}
