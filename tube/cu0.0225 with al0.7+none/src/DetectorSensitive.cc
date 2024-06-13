// DetectorSensitive.cc
#include "DetectorSensitive.hh"


MySensitiveDetector::MySensitiveDetector(G4String name) : G4VSensitiveDetector(name)
{}

MySensitiveDetector::~MySensitiveDetector()
{}

G4bool MySensitiveDetector::ProcessHits(G4Step *aStep, G4TouchableHistory *)
{
  G4StepPoint *preStepPoint = aStep->GetPreStepPoint();
  G4ThreeVector posParticle = preStepPoint->GetPosition();
  G4ThreeVector dirParticle = preStepPoint->GetMomentumDirection();
  G4double energyParticle = preStepPoint->GetKineticEnergy();
  G4double massParticle = preStepPoint->GetMass();


  //const G4VTouchable *touchable = aStep->GetPreStepPoint()->GetTouchable();
  //G4int copyNo = touchable->GetCopyNumber();
  
  //G4cout << "Copy number: " << copyNo << G4endl;

  //G4VPhysicalVolume *physVol = touchable->GetVolume();
  //G4ThreeVector posDetector = physVol->GetTranslation();
  //G4cout << "Detector position: " << posDetector << G4endl;

  G4int evt = G4RunManager::GetRunManager()->GetCurrentEvent()->GetEventID();
  
  #ifndef G4MULTITHREADED
    G4cout << "Event: " << evt << G4endl;
    G4cout << "Particle energy: " << energyParticle << G4endl;
    G4cout << "Particle mass: " << massParticle << G4endl;
  #endif
	
	
  G4AnalysisManager *man = G4AnalysisManager::Instance();
  man->FillNtupleIColumn(0, evt);
  man->FillNtupleDColumn(1, posParticle[0]);
  man->FillNtupleDColumn(2, posParticle[1]);
  man->FillNtupleDColumn(3, posParticle[2]);
  man->FillNtupleDColumn(4, dirParticle[0]);
  man->FillNtupleDColumn(5, dirParticle[1]);
  man->FillNtupleDColumn(6, dirParticle[2]);
  man->FillNtupleDColumn(7, energyParticle);
  man->FillNtupleDColumn(8, massParticle);
  man->AddNtupleRow(0);

  return true;
}
