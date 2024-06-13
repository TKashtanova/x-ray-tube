// PrimaryGeneratorAction.hh
#ifndef PrimaryGeneratorAction_hh
#define PrimaryGeneratorAction_hh

#include "G4VUserPrimaryGeneratorAction.hh"
#include "G4Event.hh"
#include "G4ParticleGun.hh"
#include "G4GeneralParticleSource.hh"
#include "G4ParticleTable.hh"
#include "G4ParticleDefinition.hh"
#include "G4ThreeVector.hh"
#include "G4SystemOfUnits.hh" 
#include "Randomize.hh"


class MyPrimaryGeneratorAction : public G4VUserPrimaryGeneratorAction
{
  public:
    MyPrimaryGeneratorAction();    
    ~MyPrimaryGeneratorAction();

    virtual void GeneratePrimaries(G4Event*);

  private:
    G4GeneralParticleSource *fParticleGun;
};

#endif

