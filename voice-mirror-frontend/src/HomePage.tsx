import PersonaCard from "./PersonaCard";
import AddPersonaCard from "./AddPersonaCard";
import avatar from "./assets/avatar.png";

export default function HomePage() {
  const personaList: any[] = [
    {
      id: 1,
      image: avatar,
      name: "Harish Kanthi",
      description:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec purus feugiat, molestie ipsum et, eleifend nunc",
    },
  ];

  return (
    <div className="flex flex-col justify-center items-center gap-5">
      <h1 className="text-5xl font-bold text-primaryText">Choose a persona.</h1>
      <div className="flex flex-col justify-center items-center gap-5">
        {personaList.map((persona) => (
          <PersonaCard persona={persona} />
        ))}
        <AddPersonaCard />
      </div>
    </div>
  );
}
