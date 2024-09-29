import { ProfileContext } from "../contexts/ProfileContext";
import { Profile } from "../models/Profile";
import { Persona } from "../models/Persona";
import { useState } from "react";
import avatar from "../assets/avatar.png";

export default function ProfileProvider({ children }: any) {
  const [profile, setProfile] = useState<Profile | undefined>(undefined);
  const [personas, setPersonas] = useState<Persona[]>([
    {
      id: "1",
      image: avatar,
      name: "Harish Kanthi",
      description:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec purus feugiat, molestie ipsum et, eleifend nunc",
    },
  ]);

  const fetchProfile = async (name: string, password: string) => {
    setProfile({
      name: name,
    });
  };

  return (
    <ProfileContext.Provider
      value={{
        profile: profile,
        personas: personas,
        handleLogin: fetchProfile,
      }}
    >
      {children}
    </ProfileContext.Provider>
  );
}
