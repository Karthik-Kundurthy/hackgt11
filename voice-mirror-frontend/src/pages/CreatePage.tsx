import PersonaForm from "../components/PersonaForm";
import { useContext } from "react";
import { ProfileContext } from "../contexts/ProfileContext";
import { Navigate } from "react-router-dom";
import { persona_create } from "../api/api";

export default function CreatePage() {
  const { profile } = useContext(ProfileContext);

  if (!profile) {
    return <Navigate to="/login" />;
  }

  const createPersona = async (
    name: string,
    description: string,
    avatar: any,
    documents: FileList,
  ) => {
    console.log(profile.username, name, description, documents);
    const reader = new FileReader();
    const files: any[] = [];
    reader.onload = async (e) => {
      const text = e.target!.result;
      files.push(text);
    };
    // iterate over documents
    for (let i = 0; i < documents.length; i++) {
      const file = documents[i];
      reader.readAsText(file);
    }
    await persona_create(profile.username, name, description, files);
  };

  return (
    <div className="flex flex-col justify-center items-center gap-5">
      <h1 className="text-5xl font-bold text-primaryText">Create a persona.</h1>
      <PersonaForm personaFormHandler={createPersona} />
    </div>
  );
}
