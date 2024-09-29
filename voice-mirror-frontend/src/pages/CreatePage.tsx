import PersonaForm from "../components/PersonaForm";
import { useContext } from "react";
import { ProfileContext } from "../contexts/ProfileContext";
import { Navigate } from "react-router-dom";

export default function CreatePage() {
  const { profile } = useContext(ProfileContext);

  if (!profile) {
    return <Navigate to="/login" />;
  }

  const createPersona = async (
    name: string,
    description: string,
    avatar: any,
    documents: any,
  ) => {};

  return (
    <div className="flex flex-col justify-center items-center gap-5">
      <h1 className="text-5xl font-bold text-primaryText">Create a persona.</h1>
      <PersonaForm personaFormHandler={createPersona} />
    </div>
  );
}
