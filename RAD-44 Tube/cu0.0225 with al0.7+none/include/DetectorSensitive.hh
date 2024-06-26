// DetectorSensitive.hh
#ifndef DetectorSensitive_hh
#define DetectorSensitive_hh

#include "G4VSensitiveDetector.hh"
#include "G4RunManager.hh"
#include "G4AnalysisManager.hh"
//#include "g4root.hh"

class MySensitiveDetector : public G4VSensitiveDetector
{
public:
  MySensitiveDetector(G4String);
  ~MySensitiveDetector();

private:
  virtual G4bool ProcessHits(G4Step *, G4TouchableHistory *);
};

#endif
