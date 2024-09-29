import PersonaCard from "../components/PersonaCard";
import AddPersonaCard from "../components/AddPersonaCard";
import avatar from "../assets/avatar.png";
import { useContext } from "react";
import { ProfileContext } from "../contexts/ProfileContext";
import { Navigate } from "react-router-dom";
import { persona_edit } from "../api/api";


export default function HomePage() {
  const { profile, personas } = useContext(ProfileContext);

  if (!profile) {
    return <Navigate to="/login" />;
  }

  return (
    <div className="flex flex-col justify-center items-center gap-5">
      <h1 className="text-5xl font-bold text-primaryText">Choose a persona.</h1>
      <div className="flex flex-col justify-center items-center gap-5">
        {personas.map((persona) => (
          <PersonaCard persona={persona} />
        ))}
        <AddPersonaCard />
      </div>
    </div>
  );
}
