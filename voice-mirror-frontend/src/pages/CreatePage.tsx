import PersonaForm from "../components/PersonaForm";
import { useContext } from "react";
import { ProfileContext } from "../contexts/ProfileContext";
import { Navigate } from "react-router-dom";
import { persona_create } from "../api/api";
import { useNavigate } from "react-router-dom";

export default function CreatePage() {
  const { profile } = useContext(ProfileContext);
  const navigate = useNavigate();

  if (!profile) {
    return <Navigate to="/login" />;
  }

  const createPersona = async (
    name: string,
    description: string,
    avatar: any,
    documents: FileList,
  ) => {
    // iterate over documents
    const promises = Array.from(documents).map((file) => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsText(file);
      });
    });

    const files: any[] = await Promise.all(promises);

    await persona_create(profile.username, name, description, files);
    navigate("/");
  };

  return (
    <div className="flex flex-col justify-center items-center gap-5">
      <h1 className="text-5xl font-bold text-primaryText">Create a persona.</h1>
      <PersonaForm personaFormHandler={createPersona} />
    </div>
  );
}
