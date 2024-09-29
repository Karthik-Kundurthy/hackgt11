import PersonaForm from "../components/PersonaForm";
import Title from "../components/Title";
import { useParams } from "react-router-dom";
import { useContext } from "react";
import { ProfileContext } from "../contexts/ProfileContext";
import { Navigate } from "react-router-dom";
import { persona_edit } from "../api/api";
import { useNavigate } from "react-router-dom";

export default function EditPage() {
  // use this id later
  const { name } = useParams();
  const { profile, personas, refreshPersonas } = useContext(ProfileContext);
  const navigate = useNavigate();
  const persona = personas.find((persona) => persona.name === name);

  if (!profile) {
    return <Navigate to="/login" />;
  }

  if (!persona) {
    return <Navigate to="/" />;
  }

  const editPersona = async (
    name: string,
    description: string,
    avatar: any,
    documents: FileList,
  ) => {
    const promises = Array.from(documents).map((file) => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsText(file);
      });
    });

    const files: any[] = await Promise.all(promises);
    await persona_edit(profile.username, name, description, files);
    await refreshPersonas(profile.username);
    navigate("/");
  };

  return (
    <div>
      <Title />
      <div className="flex flex-col justify-center items-center gap-5">
        <h1 className="text-3xl font-bold text-primaryText">Edit a persona</h1>
        <PersonaForm
          personaFormHandler={editPersona}
          name={persona.name}
          description={persona.description}
          isEdit={true}
        />
      </div>
    </div>
  );
}
