<template>
  <div class="progress-container">
    <div class="progress-wrapper">
      <div
        v-for="step in totalSteps"
        :key="step"
        class="progress-step"
        :class="{ active: step <= currentStep, completed: step < currentStep }"
      >
        <div class="step-circle">
          <svg
            v-if="step < currentStep"
            class="check-icon"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
          </svg>
          <span v-else>{{ step }}</span>
        </div>
        <div v-if="step < totalSteps" class="step-line" :class="{ active: step < currentStep }"></div>
      </div>
    </div>
    <p class="progress-text">{{ currentStep }} / {{ totalSteps }}</p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  currentStep: number;
  totalSteps: number;
}

defineProps<Props>();
</script>

<style scoped>
.progress-container {
  max-width: 600px;
  margin: 0 auto 60px;
  text-align: center;
}

.progress-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 16px;
}

.progress-step {
  display: flex;
  align-items: center;
}

.step-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #27272A;
  border: 2px solid #3F3F46;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 18px;
  color: #71717A;
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.progress-step.active .step-circle {
  background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
  border-color: #8B5CF6;
  color: white;
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
}

.progress-step.completed .step-circle {
  background: #10B981;
  border-color: #10B981;
  color: white;
}

.check-icon {
  width: 24px;
  height: 24px;
}

.step-line {
  width: 80px;
  height: 3px;
  background: #3F3F46;
  margin: 0 8px;
  transition: all 0.3s ease;
}

.step-line.active {
  background: linear-gradient(90deg, #10B981 0%, #8B5CF6 100%);
}

.progress-text {
  color: #A1A1AA;
  font-size: 14px;
  font-weight: 500;
}

@media (max-width: 640px) {
  .step-circle {
    width: 40px;
    height: 40px;
    font-size: 16px;
  }

  .step-line {
    width: 50px;
  }

  .check-icon {
    width: 20px;
    height: 20px;
  }
}
</style>