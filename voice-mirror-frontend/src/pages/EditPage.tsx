import PersonaForm from "../components/PersonaForm";
import { useParams } from "react-router-dom";
import { useContext } from "react";
import { ProfileContext } from "../contexts/ProfileContext";
import { Navigate } from "react-router-dom";

export default function EditPage() {
  // use this id later
  const { id } = useParams();
  const { profile } = useContext(ProfileContext);

  if (!profile) {
    return <Navigate to="/login" />;
  }

  return (
    <div className="flex flex-col justify-center items-center gap-5">
      <h1 className="text-5xl font-bold text-primaryText">Edit a persona.</h1>
      <PersonaForm />
    </div>
  );
}
