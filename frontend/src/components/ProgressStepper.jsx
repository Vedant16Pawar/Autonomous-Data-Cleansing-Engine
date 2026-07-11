import './ProgressStepper.css';

const STEPS = [
  'Inspecting Data',
  'Generating Code',
  'Executing in Sandbox',
  'Validating Output',
];

/**
 * Horizontal progress stepper.
 * @param {{ currentStep: number }} props — currentStep is 0-3
 */
export default function ProgressStepper({ currentStep = 0 }) {
  return (
    <div className="progress-stepper">
      <div className="progress-stepper__track">
        {STEPS.map((label, index) => {
          const isCompleted = index < currentStep;
          const isActive    = index === currentStep;
          // const isFuture = index > currentStep;

          const circleClass = isCompleted
            ? 'progress-stepper__circle--completed'
            : isActive
              ? 'progress-stepper__circle--active'
              : 'progress-stepper__circle--future';

          const labelClass = isCompleted
            ? 'progress-stepper__label--completed'
            : isActive
              ? 'progress-stepper__label--active'
              : 'progress-stepper__label--future';

          /* Connector state is based on the step to the LEFT of the line */
          let connectorClass = '';
          if (index < STEPS.length - 1) {
            if (index < currentStep) {
              connectorClass = 'progress-stepper__connector--completed';
            } else if (index === currentStep) {
              connectorClass = 'progress-stepper__connector--active';
            } else {
              connectorClass = 'progress-stepper__connector--future';
            }
          }

          return (
            <div className="progress-stepper__step" key={index}>
              {/* Circle */}
              <div className={`progress-stepper__circle ${circleClass}`}>
                {isCompleted ? '✓' : index + 1}
              </div>

              {/* Label */}
              <span className={`progress-stepper__label ${labelClass}`}>
                {label}
              </span>

              {/* Connector line (skip last step) */}
              {index < STEPS.length - 1 && (
                <div
                  className={`progress-stepper__connector ${connectorClass}`}
                />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
