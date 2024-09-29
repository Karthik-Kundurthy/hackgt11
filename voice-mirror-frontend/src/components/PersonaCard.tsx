import { MdEdit } from "react-icons/md";
import { MdChat } from "react-icons/md";
import { useNavigate } from "react-router-dom";
import { Persona } from "../models/Persona";
import avatar from "../assets/avatar.png";

export default function PersonaCard({ persona }: { persona: Persona }) {
  // typical card layout with image, title, and description and edit button
  const navigate = useNavigate();
  return (
    <div className="w-full">
      <div className="flex border-2 rounded-xl border-primaryBorder bg-secondary p-3 gap-4 h-32">
        <div className="flex flex-col justify-center">
          <img
            src={avatar}
            alt={persona.name}
            className="h-10 w-10 rounded-full"
          />
        </div>
        <div className="max-w-96 flex flex-col text-start mr-auto">
          <h2 className="text-xl font-bold">{persona.name}</h2>
          <p className="text-md">{persona.description}</p>
        </div>
        <div className="flex flex-col justify-center gap-5">
          <button
            className="pr-3 pl-3 pt-1 pb-1 rounded-xl bg-primaryButton text-primaryButtonText font-semibold flex items-center justify-evenly gap-1"
            onClick={() => {
              navigate("/chat/" + persona.name);
            }}
          >
            Chat
            <MdChat className="inline-block" />
          </button>
          <button
            className="pr-3 pl-3 pt-1 pb-1 rounded-xl bg-primaryButton text-primaryButtonText font-semibold flex items-center justify-evenly gap-1"
            onClick={() => {
              console.log("/edit/" + persona.name);
              navigate("/edit/" + persona.name);
            }}
          >
            Edit
            <MdEdit className="inline-block" />
          </button>
        </div>
      </div>
    </div>
  );
}
